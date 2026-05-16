def get_finger_states(hand_landmarks):
    tips_ids = [4, 8, 12, 16, 20]
    states = []

    # Thumb
    if hand_landmarks.landmark[tips_ids[0]].x < hand_landmarks.landmark[tips_ids[0]-1].x:
        states.append(True)
    else:
        states.append(False)

    # Fingers
    for id in tips_ids[1:]:
        if hand_landmarks.landmark[id].y < hand_landmarks.landmark[id-2].y:
            states.append(True)
        else:
            states.append(False)

    return states


GESTURES = {
    (True, False, False, False, False): "Thumbs Up 👍",
    (False, True, True, False, False): "Victory ✌️",
    (True, True, True, True, True): "Palm Open ✋",
    (False, False, False, False, False): "Fist ✊",
    (False, True, False, False, False): "Index ☝️"
}


def get_gesture(hand_landmarks):
    states = get_finger_states(hand_landmarks)
    return GESTURES.get(tuple(states), "Unknown")