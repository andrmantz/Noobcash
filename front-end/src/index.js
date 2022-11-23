import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import history from "./history";

ReactDOM.render(
  <React.StrictMode>
    <BrowserRouter History={history}>
      <Routes>
        <Route path="/"           element={<App page="" />}           />
        <Route path="/analytics"  element={<App page="analytics" />}  />
        <Route path="/actions"    element={<App page="actions" />}    />
        <Route path="/account"    element={<App page="account" />}    />
        <Route path="/login"    element={<App page="login" />}    />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
