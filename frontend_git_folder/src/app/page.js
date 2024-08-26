"use client";
import { useRouter } from 'next/navigation'; // Use next/navigation for client components
import { useEffect, useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faGooglePlusG } from "@fortawesome/free-brands-svg-icons";
import styles from './page.module.css';
import { createParticipant, fetchUserDatabyuserID, submitData } from "./api/applicationapi";
import { message } from 'antd';

export default function Home() {
  const router = useRouter(); // Use useRouter from next/navigation for client-side navigation
  const [isSignUp, setIsSignUp] = useState(false);
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [userName, setuserName] = useState("");
  const [userName2, setuserName2] = useState("");
  const [password2, setPassword2] = useState("");
  const [emailId, setEmailId] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setconfirmPassword] = useState("");
  const [mobile, setMobile] = useState("");
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetchUserDatabyuserID()
        const sessionData = await response.json();
        const usename = sessionData?.username;
        const pass = sessionData?.password;
        console.log(usename);
        console.log(pass);
        setuserName2(usename);
        setPassword2(pass);
        console.log(userName2);
        console.log(password2);
        // const userData = await getTarget(accessToken);
        // setUserId(userData?.results[0]?.id);
      } catch (e) {
        console.log("Error", e);
      }
    };
    fetchData();
  }, []);
  const toggleForm = () => {
    setIsSignUp(!isSignUp);
  };

  const handleSave = async (event) => {
  event.preventDefault();

  // Basic Validation Checks
  if (!firstName || !lastName || !userName || !emailId || !password || !confirmPassword || !mobile) {
    message.error("All fields are required");
    return;
  }

  // Mobile Number Validation
  const mobileRegex = /^\d{10}$/;
  if (!mobileRegex.test(mobile)) {
    message.error("Mobile number must contain exactly 10 digits");
    return;
  }

  // Email Validation
  const emailRegex = /^[a-zA-Z0-9._%+-]+@gmail\.com$/;
  if (!emailRegex.test(emailId)) {
    message.error("Please Enter Valid Email Address");
    return;
  }

  const requestBody = {
    first_name: firstName,
    last_name: lastName,
    username: userName,
    email_id: emailId,
    password: password,
    confirm_password: confirmPassword,
    mobile_number: mobile,
  };

  console.log(requestBody);
  
  try {
    const submitResponse = await createParticipant(requestBody);
    console.log(submitResponse);

    if (submitResponse === "username not available try another") {
      message.error(`${userName} not available`);
    } else if (submitResponse === "password doesnot match please try again") {
      message.error("Password and Confirm Password do not match");
    } else {
      message.success(`${userName} registered successfully`);
    }
  } catch (error) {
    console.error("Error submitting data:", error);
  }
};


const handleLogin = async (event) => {
  event.preventDefault();
  
  const requestBody = { 
    username: userName,
    password: password,
  };
  console.log(requestBody);

  try {
    const submitResponse = await submitData(requestBody);
    console.log(submitResponse);

    // Check if the login was successful based on the actual response
    if (submitResponse === "user logged in sucessfully") {  // Adjust this condition based on your API response structure
      message.success(`${userName} logged in successfully`);
      console.log("Login Successful");
      router.push('/home'); // Redirect to the home page
    } else {
      message.error("Invalid Credentials");
      console.error("Invalid login credentials");
    }
  } catch (error) {
    console.error("Error submitting data:", error);
  }
};

  return (
    <main className={styles.main}>
      <div className={`${styles.container} ${isSignUp ? styles.active : ""}`} id="container">
        <div className={`${styles["form-container"]} ${styles["sign-up"]}`}>
          <form>
            <h1>Create Account</h1>
            <div className={styles["social-icons"]}>
              <a href="#" className={styles.icon}>
                <FontAwesomeIcon icon={faGooglePlusG} />
              </a>
            </div>
            <span>or use your email for registration</span>
            <input type="text" placeholder="First Name" onChange={(e)=>{
                 setFirstName(e.target.value)
            }} required />
            <input type="text" placeholder="Last Name" onChange={(e)=>{
                 setLastName(e.target.value)
            }} required />
            <input type="text" placeholder="Username" onChange={(e)=>{
                  setuserName(e.target.value)
            }} required />
            <input type="email" placeholder="Email" onChange={(e)=>{
                     setEmailId(e.target.value)
            }} required />
            <input type="password" placeholder="Password"onChange={(e)=>{
                     setPassword(e.target.value)
            }} required />
            <input type="password" placeholder="Confirm Password" onChange={(e)=>{
                     setconfirmPassword(e.target.value)
            }} required />
            <input type="tel" placeholder="Mobile Number" onChange={(e)=>{
                     setMobile(e.target.value)
            }}  required />
            <button onClick={handleSave}>Sign Up</button>
          </form>
        </div>
        <div className={`${styles["form-container"]} ${styles["sign-in"]}`}>
          <form>
            <h1>Sign In</h1>
            <div className={styles["social-icons"]}>
              <a href="#" className={styles.icon}>
                <FontAwesomeIcon icon={faGooglePlusG} />
              </a>
            </div>
            <span>or use your email password</span>
            <input type="text" id="Username" placeholder="Username" onChange={(e)=>{
                 setuserName(e.target.value)
            }} required />
            <input type="password" placeholder="Password" onChange={(e)=>{
                 setPassword(e.target.value)
            }} required />
            <a href="#">Forget Your Password?</a>
            <button onClick={handleLogin}>Sign In</button>
          </form>
        </div>
        <div className={styles["toggle-container"]}>
          <div className={styles.toggle}>
            <div className={`${styles["toggle-panel"]} ${styles["toggle-left"]}`}>
              <h1>PHARMAREGTECH PVT LTD!</h1>
              <p>Enter your personal details to use all of site features</p>
              <button className={styles.hidden} onClick={toggleForm} id="login">Sign In</button>
            </div>
            <div className={`${styles["toggle-panel"]} ${styles["toggle-right"]}`}>
              <h1>PHARMAREGTECH PVT LTD</h1>
              <p>Register with your personal details to use all of site features</p>
              <button className={styles.hidden} onClick={toggleForm} id="register">Sign Up</button>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
