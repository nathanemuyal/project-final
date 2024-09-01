import './style/App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Selected from './pages/Selected';
import Personalised from './pages/Personalised';
import Result from './pages/Result';
import PrivateRoute from './component/PrivateRoute';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path='/' element={<Home />} />
          <Route path='/Selected' element={
            <PrivateRoute>
              <Selected />
            </PrivateRoute>
          } />
          <Route path='/Personalised' element={
            <PrivateRoute>
              <Personalised />
            </PrivateRoute>
          } />
          <Route path='/Result' element={
            <PrivateRoute>
              <Result />
            </PrivateRoute>
          } />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
