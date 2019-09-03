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

## Interactive story - 4

* greet
    - utter_greet
* complaint
    - complaint_form
    - form{"name":"complaint_form"}
    - slot{"requested_slot":"category"}
* complaint{"category":"internet banking"}
    - complaint_form
    - slot{"category":"internet banking"}
    - slot{"requested_slot":"complaint_text"}
* complaint
    - complaint_form
    - slot{"complaint_text":"I am unable to login to my bank account. Can you help me reset my password?"}
    - form{"name":null}
    - slot{"requested_slot":null}
    - utter_confirmation
    - action_restart

## Interactive story - 5

* greet
    - utter_greet
* complaint
    - complaint_form
    - form{"name":"complaint_form"}
    - slot{"requested_slot":"category"}
* complaint{"category":"service charges"}
    - complaint_form
    - slot{"category":"service charges"}
    - slot{"requested_slot":"complaint_text"}
* track
    - complaint_form
    - slot{"complaint_text":"I believe the service charges for my last transactions are too high. I would like to have a word with the manager."}
    - form{"name":null}
    - slot{"requested_slot":null}
    - utter_confirmation
    - action_restart


## Interactive story - 6

* complaint{"category":"loans"}
    - complaint_form
    - form{"name":"complaint_form"}
    - slot{"category":"loans"}
    - slot{"requested_slot":"complaint_text"}
* track
    - complaint_form
    - slot{"complaint_text":"I am unable to process my loan papers."}
    - form{"name":null}
    - slot{"requested_slot":null}
    - utter_confirmation
    - action_restart
 * complaint
     - complaint_form
     - form{"name":"complaint_form"}
     - slot{"requested_slot":"category"}
 * complaint{"category":"cheques and drafts"}
     - complaint_form
     - slot{"category":"cheques and drafts"}
     - slot{"requested_slot":"complaint_text"}
 * track
     - complaint_form
     - slot{"complaint_text":"My last cheque just bounced. I believe that is a mistake."}
     - form{"name":null}
     - slot{"requested_slot":null}
     - utter_confirmation
     - action_restart

## Interactive story - 7
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