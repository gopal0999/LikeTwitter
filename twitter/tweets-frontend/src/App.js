import './App.css';
import React, {useEffect, useState} from 'react';

function loadTweets(callback) {
  const xhr = new XMLHttpRequest()
  const method = 'GET' // "POST"
  const url = "http://localhost:8000/api/tweets/"
  const responseType = "json"
  xhr.responseType = responseType
  xhr.open(method, url)
  xhr.onload = function() {
    callback(xhr.response, xhr.status)
  }
  xhr.onerror = function (e) {
    console.log(e)
    callback({"message": "The request was an error"}, 400)
  }
  xhr.send()
}


function App() {
  const [tweets, setTweets] = useState([])
 
  useEffect(() => {
    const myCallback = (response, status) => {
      console.log(response, status)
      if (status === 200){
        setTweets(response)
      } else {
        alert("There was an error")
      }
    }
    loadTweets(myCallback)
  }, [])
  return (
    <div className="App">
        <p>
          {tweets.map((tweet, index)=>{
            return <li>{tweet.content}</li>
          })}
        </p>
    </div>
  );
}

export default App;
