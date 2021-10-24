
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

8/04
- Created a customers blueprints to interact with mongodb

9/04
- Added loading spinner during ajax call 

15/04
- Blling GCS


20/04
- Create multiple env and multiple db/twilio account for a demo


25/04
- Pagination
- Moved customers and paginations methods from routes.py to pagination.oy and customer.py"


9/05
- Script to deploy automaticly the app on Google Cloud Run


22/05
- Added domain name of the pagination (SEO friendly way)
- Displayed the number of customers of the cusomters tab


29/05
- Added front-end validation when adding a new user (following an incredible JS tutorial available [here](https://www.javascripttutorial.net/javascript-dom/javascript-form-validation/))
- Fixed a minor bug (typo) to delete a customer 


29/06
- Fixed the technical documentation (typo)
- Fixed a duplication issue when adding a new user in the customers list 


23/10
- Update deploy.sh script to deploy the app on GCP in a cleaner way


24/10
- Added a linter job and a build_and_deploy job on the CI/CD pipeline


TODO
- Fix issue with SMS error 