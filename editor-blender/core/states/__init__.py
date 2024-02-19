from ..models import (
    Clipboard,
    ColorMapPending,
    ColorMapUpdates,
    ControlMapUpdates,
    CopiedType,
    EditingData,
    EditMode,
    Editor,
    LEDMapPending,
    LEDMapUpdates,
    PosMapUpdates,
    SelectMode,
    State,
)

state = State(
    running=False,
    sync=False,
    logged_in=False,
    playing=False,
    requesting=False,
    subscription_task=None,
    init_editor_task=None,
    command_task=None,
    assets_path="",
    token="",
    username="",
    ready=False,
    control_map={},
    pos_map={},
    control_record=[],
    pos_record=[],
    # TODO: Add these
    led_map={},
    led_effect_id_table={},
    current_control_index=0,
    current_pos_index=0,
    current_led_index=0,
    # NOTE: Maybe we don't need these
    current_fade=False,
    current_status={},
    current_pos={},
    # current_editing_frame=-1,
    current_editing_frame=0,
    current_editing_detached=False,
    current_editing_frame_synced=True,
    # NOTE: Guess we can't implement these
    # status_stack=[],
    # status_stack_index=0,
    # pos_stack=[],
    # pos_stack_index=0,
    # TODO: Add these
    # led_effect_record={},
    # current_led_status={}
    edit_state=EditMode.IDLE,
    editor=Editor.CONTROL_EDITOR,
    local_view=False,
    editing_data=EditingData(frame_id=-1, start=0, index=0),
    shifting=False,
    # NOTE: Guess we can't implement these
    selection_mode=SelectMode.PART_MODE,
    selected_obj_names=[],
    selected_obj_type=None,
    clipboard=Clipboard(CopiedType.NONE),
    models={},
    model_names=[],
    models_array=[],
    model_dancer_index_map={},
    dancers={},
    dancer_names=[],
    dancers_array=[],
    dancer_part_index_map={},
    part_type_map={},
    led_part_length_map={},
    color_map={},
    # effect_list
    rpi_status={},
    shell_history={},
    color_map_updates=ColorMapUpdates(added=[], updated=[], deleted=[]),
    color_map_pending=ColorMapPending(add_or_delete=False, update=False),
    led_map_updates=LEDMapUpdates(added=[], updated=[], deleted=[]),
    led_map_pending=LEDMapPending(add_or_delete=False, update=False),
    control_map_updates=ControlMapUpdates(added=[], updated=[], deleted=[]),
    control_map_pending=False,
    pos_map_updates=PosMapUpdates(added=[], updated=[], deleted=[]),
    pos_map_pending=False,
)
