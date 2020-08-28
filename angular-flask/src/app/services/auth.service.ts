import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { User, Login, UserNoPW } from "../models/User";
import { JwtHelperService } from "@auth0/angular-jwt";
import { Observable } from "rxjs";

const httpOptions = {
  headers: new HttpHeaders({
    "Content-Type": "application/json",
  }),
};

@Injectable({
  providedIn: "root",
})
export class AuthService {
  authToken: any;
  user: User;
  login: Login;
  userNoPW: UserNoPW;

  constructor(private http: HttpClient, public jwtHelper: JwtHelperService) {}

  registerUser(user): Observable<any> {
    const registerUrl = this.prepEndpoint("static/users/register");
    return this.http.post(registerUrl, user, httpOptions);
  }

  authenticateUser(login): Observable<any> {
    const loginUrl = this.prepEndpoint("static/users/authenticate");
    return this.http.post(loginUrl, login, httpOptions);
  }



  getList(): Observable<any> {
    const listUrl = this.prepEndpoint("static/users/list");
    return this.http.get(listUrl, httpOptions);
  }

  storeUserData(token, userNoPW) {
    localStorage.setItem("idtoken", token);
    localStorage.setItem("user", JSON.stringify(userNoPW));
    this.authToken = token;
    this.userNoPW = userNoPW;
  }
  logout() {
    this.authToken = null;
    this.userNoPW = null;
    localStorage.clear();
  }
  loggedIn() {
    return !this.jwtHelper.isTokenExpired(this.authToken);
  }
  sendImageDecode(data): Observable<any> {
    const sendImage = this.prepEndpoint("static/image/decodeImage");

    return this.http.post(sendImage, data, httpOptions);
  }
  prepEndpoint(ep) {
    return "http://localhost:9999/" + ep;
    //return ep;
  }
}
