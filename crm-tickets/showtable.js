function fetchTargetedSentiment() {

    let myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    let rid = document.getElementById("rid").value;

    let body = { "reviewId" : rid};
    let raw = JSON.stringify(body);
    console.log(raw);

    var requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: raw,
      redirect: 'follow'
    };

    apiGwUrl = 'url must end in /targeted';

    fetch(apiGwUrl, requestOptions)
      .then(response => response.json())
      .then(result => showTargetedSentiment(result.body.Items))
      .catch(error => console.log('error', error));
  }

showTargetedSentiment = (entities) => {
    console.log(entities);
    let entitiesDiv = document.querySelector("#list-of-entities");

    if (entities == "error") {
      errorHtml = '<p class="entities-failure">Session timed out. Please logout and login again!</p>';
      entitiesDiv.innerHTML = errorHtml;
      sessionStorage.clear();
      return;
    }

    let myEntityList = [];
    entities.forEach(item => {
      //let reviewId = item.reviewId.S;
      let entity = item.entity.S;
      let ageGroup = item.ageGroup.S;
      let author = item.author.S;
      let beginOffset = item.beginOffset.S;
      let entityType = item.entityType.S;
      let entityId = item.entityId.N;
      let gender = item.gender.S;
      let review = item.review.S;
      let sentiment = item.sentiment.S;
      let sentimentScore = item.sentimentScore.S;
      let state= item.state.S;
      let timeStamp = item.timeStamp.N;

      let myEntity = {
        //"Review ID" : reviewId,
        "Entity" : entity,
        "Sentiment" : sentiment,
        "Sentiment Score" : sentimentScore,
        "Age Group" : ageGroup,
        "Author" : author,
        "Begin Offset" : beginOffset,
        "Entity Type" : entityType,
        "Entity ID" : entityId,
        "Gender" : gender,
        "State" : state,
        "Timestamp" : timeStamp, 
        "Review" : review,
      }
      
      myEntityList.push(myEntity);
    })

    console.log(myEntityList);

    if (myEntityList.length > 0) {
      let table = document.createElement('table');
      table.classList.add('entitiestable');
      let header = Object.keys(myEntityList[0]);
      generateTable(table, myEntityList);
      generateTableHead(table, header);
      console.log(table);
      entitiesDiv.appendChild(table);
    } else {
      errorHtml = '<p class="events-failure">No reviews found!</p>';
      entitiesDiv.innerHTML = errorHtml;
    }

    ticketHtml = '<button class="button" onclick="return doLogout()">Create Ticket</button>';
    const ticketDiv = document.querySelector("#ticket-button");
    ticketDiv.innerHTML = ticketHtml;
  }

function generateTableHead(table, data) {
    let thead = table.createTHead();
    let row = thead.insertRow();
    for (let key of data) {
      let th = document.createElement("th");
      let text = document.createTextNode(key);
      th.appendChild(text);
      row.appendChild(th);
    }
  }

function generateTable(table, data) {
    for (let element of data) {
      let row = table.insertRow();
      for (key in element) {
        let cell = row.insertCell();
        let text = document.createTextNode(element[key]);
        cell.appendChild(text);
      }
    }
  }
