import React, { useState } from 'react';

const LoginForm = ({ switchForm }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    const response = await fetch('http://localhost:8000/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: `username=${username}&password=${password}`,
    });

    if (response.ok) {
      const data = await response.json();
      console.log('Login successful');
      console.log('Access Token:', data.access_token);
    } else {
      alert('Login failed');
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleLogin}>Login</button>
      <p>
        Don't have an account?{' '}
        <button onClick={() => switchForm('register')}>Register</button>
      </p>
    </div>
  );
};

const RegisterForm = ({ switchForm }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');

  const registerUser = async () => {
    const response = await fetch('/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username,
        password: password,
        email: email,
      }),
    });

    if (response.ok) {
      console.log('User registered successfully');
    } else {
      const data = await response.json();
      console.error(data.detail);
    }
  };

  return (
    <div>
      <h2>Register</h2>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <input
        type="text"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <button onClick={registerUser}>Register</button>
      <p>
        Already have an account?{' '}
        <button onClick={() => switchForm('login')}>Login</button>
      </p>
    </div>
  );
};

const App = () => {
  const [formType, setFormType] = useState('login');

  const switchForm = (form) => {
    setFormType(form);
  };

  return (
    <div>
      {formType === 'login' && <LoginForm switchForm={switchForm} />}
      {formType === 'register' && <RegisterForm switchForm={switchForm} />}
    </div>
  );
};

export default App;
