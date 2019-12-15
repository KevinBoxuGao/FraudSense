import React, {createContext, useContext} from "react";

interface UserContext {
    user?: firebase.User;
    initialising?: boolean;
  }
  
  export const userContext = React.createContext<UserContext>({
    user: undefined
  });

export const useSession = () => {
    const { user } = useContext(userContext)
    return user
}