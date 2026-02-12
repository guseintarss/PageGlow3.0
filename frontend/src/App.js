import logo from './logo.svg';
import './App.css';
import { Routes, Route } from 'react-router-dom';


import React, { useState, useEffect } from 'react';
import axios from 'axios';


function ArticleList() {
  const [articles, setArticles] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:8000/api/articles/')
      .then(response => {
        console.log('Данные из API:', response.data); // Проверьте в консоли
        setArticles(response.data.results);
      })
      .catch(err => {
        console.error('Ошибка запроса:', err);
        setError(err.message);
      });
  }, []);

  if (error) return <div>Ошибка: {error}</div>;

  return (
    <div>
      {articles.map(article => (
        <div key={article.id}>
          <h2>{article.title}</h2>
          <p>{article.content}</p>
        </div>
      ))}
    </div>
  );
}


export default App;
