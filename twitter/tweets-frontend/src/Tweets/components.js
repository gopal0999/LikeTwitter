import React, {useEffect,useState} from 'react'

import {loadTweets} from '../Lookup'

export TweetsList = (props) => {
    const [tweets, setTweets] = useState([])
    useEffect(() => {

    },[])
    return <div className='tweet-list'>{tweets.map((tweet,index) => {
        <Tweet tweet={tweet} className='Tweet' key={`${index}-{tweet.id}`}/>
    })}</div>
}