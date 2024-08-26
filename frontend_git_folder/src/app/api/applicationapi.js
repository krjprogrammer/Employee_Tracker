
const baseUrl ="http://127.0.0.1:4000/"

export const createParticipant = async (requestData) => {
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
         
      },
      body: JSON.stringify(requestData),
    };
  
    const response = await fetch(`${baseUrl}register`, requestOptions);
  
    if (!response.ok) {
      const statusText = await response.text();
      const additionalMessages = [
        "The fields user, relation_with must make a unique set",
        "user_cant_be_a_relative_with_self",
      ];
  
      additionalMessages.forEach(searchTerm => {
        if (statusText.includes(searchTerm)) {
          message.error(searchTerm);
        } else {
          console.error(statusText);
        }
      });
  
      return false;
    } else {
      const data = await response.json();
      return data;
    }
  };
  
  
export const submitData = async (requestData) => {
  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",   
    },
    body: JSON.stringify(requestData),
  };

  const response = await fetch(`${baseUrl}login`, requestOptions);

  if (!response.ok) {
    const statusText = await response.text();
    const additionalMessages = [
      "The fields user, relation_with must make a unique set",
      "user_cant_be_a_relative_with_self",
    ];

    additionalMessages.forEach(searchTerm => {
      if (statusText.includes(searchTerm)) {
        message.error(searchTerm);
      } else {
        console.error(statusText);
      }
    });

    return false;
  } else {
    const data = await response.json();
    return data;
  }
};
export const fetchUserDatabyuserID = async () => {
  const userApiUrl = `${baseUrl}get_user_data`; // Use template literals correctly
  try {
    const userResponse = await fetch(userApiUrl, {
      headers: {
         // Correctly interpolate the accessToken
        "Content-Type": "application/json",
      },
    });

    if (userResponse.status === 401) {
      return null; // Handle unauthorized access
    }

    const userDataResponse = await userResponse.json();
    return userDataResponse;
  } catch (error) {
    console.error("Error fetching user data:", error);
    throw error; // Propagate the error for the caller to handle
  }
};
