# -*- coding: utf-8 -*-
"""Use stories make init state."""

from .dialog_state import DialogState


def make_init_state(stories):
    """Use stroies create an init state."""
    informable_slots = stories['user_slot']
    requestable_slots = stories['sys_slot']
    slots = []
    for islot in informable_slots:
        slots.append({
            'type': 'informable',
            'name': islot,
            'index': len(slots),
            'value': None,
        })
    for rslot in requestable_slots:
        slots.append({
            'type': 'requestable',
            'name': rslot,
            'index': len(slots),
            'value': None,
        })
    init_state = DialogState(
        stories['user_domain'],
        stories['user_intent'],
        stories['sys_intent'],
        slots
    )
    return init_state
