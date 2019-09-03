## Greet
* greet
    - utter_greet

## complaint path
* complaint
    - complaint_form
    - form{"name" : "complaint_form"}
    - form{"name" : "null"} 
    - utter_confirmation
    - action_restart

## tracking path
* track
    - tracking_form
    - form{"name" : "tracking_form"}
    - form{"name" : "null"}
    - action_restart

## thanks path 1
* thanks
- utter_anything_else
- action_restart

## bye path 1
* bye
- utter_bye
- action_restart

## Interactive story-1

* greet
    - utter_greet
* complaint
    - complaint_form
    - form{"name":"complaint_form"}
    - slot{"requested_slot":"category"}
* complaint{"category":"card transactions"}
    - complaint_form
    - slot{"category":"card transactions"}
    - slot{"requested_slot":"complaint_text"}
* complaint{"category":"card transactions"}
    - complaint_form
    - slot{"category":"card transactions"}
    - slot{"complaint_text":"unable to do card card transactions"}
    - form{"name":null}
    - slot{"requested_slot":null}
    - utter_confirmation
    - action_restart

## Interactive story-2

* complaint
    - complaint_form
    - form{"name":"complaint_form"}
    - slot{"requested_slot":"category"}
* complaint{"category":"service charges"}
    - complaint_form
    - slot{"category":"service charges"}
    - slot{"requested_slot":"complaint_text"}
* track{"category":"service charges"}
    - complaint_form
    - slot{"category":"service charges"}
    - slot{"complaint_text":"Too high service charges."}
    - form{"name":null}
    - slot{"requested_slot":null}
    - utter_confirmation
    - action_restart

## Interactive story-3

* track
    - tracking_form
    - form{"name":"tracking_form"}
    - slot{"requested_slot":"tracking_id"}
* track{"tracking_id":"123"}
    - tracking_form
    - slot{"tracking_id":"123"}
    - form{"name":null}
    - slot{"requested_slot":null}
    - tracking_form
    - form{"name":"tracking_form"}
    - slot{"tracking_id":"123"}
    - form{"name":null}
    - slot{"requested_slot":null}
* track{"tracking_id":"318"}
    - tracking_form
    - form{"name":"tracking_form"}
    - slot{"tracking_id":"123"}
    - slot{"tracking_id":"318"}
    - form{"name":null}
    - slot{"requested_slot":null}
    - action_restart