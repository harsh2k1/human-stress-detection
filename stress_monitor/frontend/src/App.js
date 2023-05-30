import "bootstrap/dist/js/bootstrap.bundle.min.js";
import { useState } from "react";
import React, { useContext } from "react";
import { UserContext } from "./UserContext";
import "./App.css";

const DashboardForm = ({ switchForm, userid }) => {
  const iframesrc =
    "http://localhost:5601/app/dashboards#/view/e04a8880-e9ca-11ed-8966-8bdea4ff170e?_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:'2023-05-04T09:15:00.000Z',to:'2023-05-04T09:30:00.000Z'))&_a=(description:'',filters:!(('$state':(store:appState),meta:(alias:!n,disabled:!f,index:cc000000-e9c3-11ed-924c-ab74a12c118a,key:userid,negate:!f,params:(query:user1),type:phrase),query:(match_phrase:(userid:" +
    userid +
    ")))),fullScreenMode:!f,options:(hidePanelTitles:!f,useMargins:!t),query:(language:kuery,query:''),timeRestore:!f,title:'Heart%20Data%20Analysis',viewMode:view)";
  
    return (
    <div className="container">
      <h2 className="card-title text-center" style={{margin: "2rem"}} >Dashboard</h2>
      <div className="d-flex justify-content-end mb-3">
        <button className="btn btn-primary btn-block" onClick={() => switchForm('login')} style={{margin: "3rem"}}>
          Logout
        </button>
      </div>
      <iframe src={iframesrc} title="Dashboard" width="100%" height="600px"></iframe>
    </div>
  );
};

const LoginForm = ({ switchForm }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [accessToken, setAccessToken] = useState("");
  const [loginSuccess, setLoginSuccess] = useState("");
  const [hitConsume, setHitConsume] = useState(true);
  const { userId, setUserId } = useContext(UserContext);

  const handleLogin = async () => {
    const response = await fetch("http://localhost:8000/login", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: `username=${username}&password=${password}`,
    });

    if (response.ok) {
      const data = await response.json();
      console.log("Login successful");
      console.log("Access Token:", data.access_token);
      setLoginSuccess(true);
      setAccessToken(data.access_token);
      setUserId(data.userId);
      switchForm("dashboard");

      if (hitConsume) {
        setHitConsume(false)
        const response = await fetch("http://localhost:8002/consumeData", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: username }),
      });

      }

    } else {
      alert("Invalid Username or Password");
    }
  };

  return (
    <div className="container mt-5">
      <div className="card mx-auto" style={{ width: "18rem" }}>
        <div className="card-body">
          <h2 className="card-title text-center">Login</h2>
          <form>
            <div className="mb-3">
              <input
                type="text"
                className="form-control"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
            <div className="mb-3">
              <input
                type="password"
                className="form-control"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <button
              type="button"
              className="btn btn-primary btn-block"
              onClick={handleLogin}
            >
              Login
            </button>
          </form>
          {loginSuccess && (
            <div className="mt-3">
              <p>Login successful</p>
              <p>Access Token: {accessToken}</p>
            </div>
          )}
          <p className="text-center">
            Don't have an account?{" "}
            <button
              type="button"
              className="btn btn-link"
              onClick={() => switchForm("register")}
            >
              Register
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

const RegisterForm = ({ switchForm }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [registrationSuccess, setRegistrationSuccess] = useState("");

  const registerUser = async () => {
    const response = await fetch("http://localhost:8000/createUser", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        password: password,
        email: email,
      }),
    });

    if (response.ok) {
      console.log("User registered successfully");
      setRegistrationSuccess(true);
    } else {
      const data = await response.json();
      console.error(data.detail);
    }
  };

  if (registrationSuccess) {
    return (
      <div className="container">
        <h2>Registration Successful</h2>
        <p>
          User registered successfully. You can now <a href="/login">Login</a>.
        </p>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="card mx-auto" style={{ width: "50rem", padding: "2rem", margin: "5rem"}}>
        <h2>Register</h2>
        <div className="mb-3">
          <label htmlFor="username" className="form-label">
            Username
          </label>
          <input
            type="text"
            className="form-control"
            id="username"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label">
            Password
          </label>
          <input
            type="password"
            className="form-control"
            id="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="email" className="form-label">
            Email
          </label>
          <input
            type="text"
            className="form-control"
            id="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <button className="btn btn-primary" onClick={registerUser}>
          Register
        </button>
        <p>
          Already have an account?{" "}
          <button className="btn btn-link" onClick={() => switchForm("login")}>
            Login
          </button>
        </p>
      </div>
    </div>
  );
};

const App = () => {
  const [formType, setFormType] = useState("login");
  const { userId, setUserId } = useContext(UserContext);

  const switchForm = (form) => {
    setFormType(form);
  };

  return (
    <div>
      {formType === "login" && <LoginForm switchForm={switchForm} />}
      {formType === "register" && <RegisterForm switchForm={switchForm} />}
      {formType === "dashboard" && (
        <DashboardForm switchForm={switchForm} userid={userId} />
      )}
    </div>
  );
};

export default App;
