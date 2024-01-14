use crate::global;
use axum::{
    extract::Query,
    headers::{HeaderMap, HeaderValue},
    http::StatusCode,
    response::Json,
};
use http::header::CONTENT_TYPE;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Deserialize, Serialize)]
pub struct Frame {
    start: i32,
    fade: bool,
    status: HashMap<String, [i32; 4]>,
}

pub type GetDataResponse = Vec<Frame>;

#[derive(Debug, Deserialize, Serialize)]
pub struct GetDataFailedResponse {
    err: String,
}

#[derive(Debug)]
struct Color {
    r: i32,
    g: i32,
    b: i32,
}

pub async fn get_dancer_fiber_data(
    Query(query): Query<HashMap<String, String>>,
) -> Result<
    (StatusCode, (HeaderMap, Json<GetDataResponse>)),
    (StatusCode, Json<GetDataFailedResponse>),
> {
    let dancer = match query.get("dancer") {
        Some(dancer) => dancer,
        None => {
            return Err((
                StatusCode::BAD_REQUEST,
                Json(GetDataFailedResponse {
                    err: "Dancer name is required.".to_string(),
                }),
            ))
        }
    };

    let clients = global::clients::get();
    let mysql_pool = clients.mysql_pool();

    let colors = sqlx::query!(
        r#"
            SELECT Color.r, Color.g, Color.b, Color.id
            FROM Color
            "#,
    )
    .fetch_all(mysql_pool)
    .await
    .unwrap();

    // create hasmap for color
    let mut color_map: HashMap<i32, Color> = HashMap::new();
    for color in colors.iter() {
        color_map.insert(
            color.id,
            Color {
                r: color.r,
                g: color.g,
                b: color.b,
            },
        );
    }

    let data = sqlx::query!(
        r#"
            SELECT ControlFrame.id, ControlFrame.start, ControlFrame.fade, ControlData.color_id, ControlData.alpha, Part.name
            FROM controlFrame
            INNER JOIN ControlData ON ControlFrame.id = ControlData.frame_id
            INNER JOIN Part ON ControlData.part_id = Part.id
            INNER JOIN Dancer ON Part.dancer_id = Dancer.id
            WHERE Dancer.name = ? AND Part.type = 'FIBER'
            ORDER BY ControlFrame.start ASC
            "#,
        dancer
    ).fetch_all(mysql_pool)
    .await
    .unwrap();

    let mut frames = HashMap::new();

    for frame in data.iter() {
        let color = color_map
            .get(&frame.color_id.unwrap())
            .unwrap_or(&Color { r: 0, g: 0, b: 0 });

        frames
            .entry(frame.start)
            .or_insert(Frame {
                start: frame.start,
                fade: frame.fade != 0,
                status: HashMap::new(),
            })
            .status
            .insert(frame.name.clone(), [color.r, color.g, color.b, frame.alpha]);
    }

    let response: Vec<Frame> = frames.into_values().collect();

    let mut headers = HeaderMap::new();
    headers.insert(CONTENT_TYPE, HeaderValue::from_static("application/json"));

    Ok((StatusCode::OK, (headers, Json(response))))
}
