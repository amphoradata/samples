import {Actions} from 'react-amphora'

export const actionLogger = (action: Actions.Action | Actions.ActionResult, payload?: any): void => {
    console.log(action.type)
    if(payload) {
        console.log(`Payload: ${JSON.stringify(payload)}`)
    }
}
