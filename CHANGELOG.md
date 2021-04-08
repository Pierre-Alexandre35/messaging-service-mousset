
## Roadmap
- Issue: update the estimate total cost for a text-messaging campaign on the UI while minimizing the number of AJAX calls
- There is 2 user factors that affect that price: 
    --> client list: because the number of client change based on the list
    --> message length: as twilio message length 

- Modulo can work but what happends if the client copy/ paste a message? It won't work 


not working 
```  
if (
    (currentMessageLength > previousMessageLength &&
      currentMessageLength >= SegmentCharactersLimit) ||
    (currentMessageLength < previousMessageLength &&
      currentMessageLength < SegmentCharactersLimit)
  ) {
```


new algo:
- A segment is a key factor to calculate the cost of a campaign. An individual segment represent a message between 0 and 160 characters. If a message contains 500 characters for example, we will need 4 segments: 500 / 160 = 3.125 and we need to ceil this number to the nearest int. 
- The goal of this function is therefore to check whenever there is a change in the current segment number. If there is a change, we can make an AJAX call 
function updateMessage(body, SegmentCharactersLimit) {
  var messageContent = body.value;
  inputMessageLength = messageContent.length;
  updateSegmentMessage(inputMessageLength, SegmentCharactersLimit);
  
  var newSegment = Math.ceil(inputMessageLength / SegmentCharactersLimit)
  if(newSegment != currentSegment){
    updateSegmentNumber(newSegment);
    updateCost();
  }
}

- Added currency
- Docker 