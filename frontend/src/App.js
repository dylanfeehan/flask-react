import logo from './logo.svg';
import {useState, useEffect} from 'react';
import './App.css';

function App() {
  const [books, setBooks] = useState([])

  useEffect(() => {
    fetch('http://127.0.0.1:5000/getdata/', {
      'method': 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(resp => resp.json())
    .then(resp => setBooks(resp)) // the state hook method
    .then(error => console.log(error))
  }, [])

  return (
    <div className="App">
      <h1>Flask and ReactJS course</h1>
      {books.map(book => {
        return (
          <div key={books.id}>
            <h2>{book.title}</h2>
            <p>{book.body}</p>
            <p>{book.date}</p>
          </div>
        )
      })}
    </div>
  );
}

export default App;
