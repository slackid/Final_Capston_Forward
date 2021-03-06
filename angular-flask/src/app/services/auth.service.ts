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
  registerAdmin(user): Observable<any> {
    const registerUrl = this.prepEndpoint("static/admins/register");
    return this.http.post(registerUrl, user, httpOptions);
  }

  authenticateUser(login): Observable<any> {
    const loginUrl = this.prepEndpoint("static/users/authenticate");
    return this.http.post(loginUrl, login, httpOptions);
  }

  authenticateAdmin(login): Observable<any> {
    const loginUrl = this.prepEndpoint("static/admin/authenticateAdmin");
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
  rootloggedIn() {
    //루트 로그인 확인 알고리즘 추가필요
    return !this.jwtHelper.isTokenExpired(this.authToken);
  }

  checkadmin() {
    this.authToken = localStorage.getItem("idtoken");
    const httOptions1 = {
      headers: new HttpHeaders({
        "Content-Type": "application/json",
        Authorization: "Bearer " + this.authToken,
      }),
    };
    const checkingUrl = this.prepEndpoint("static/admin/check");
    return this.http.get(checkingUrl, httOptions1);
  }

  sendImageDecode(data): Observable<any> {
    const sendImage = this.prepEndpoint("static/image/decodeImage");
    return this.http.post(sendImage, data, httpOptions);
  }
  getImageEncode(usernum, username, date): Observable<any> {
    const getEncodeImage = this.prepEndpoint("/static/image/encode/send");
    const data = [
      {
        stu_num: usernum,
        name: username,
        date: date,
      },
    ];

    return this.http.post(getEncodeImage, data, httpOptions);
  }
  getSubjectData(user): Observable<any> {
    const getSubjectURL = this.prepEndpoint("static/subject/info");
    return this.http.post(getSubjectURL, user, httpOptions);
  }

  postAttendData(week, usernum): Observable<any> {
    const postAttendDataURL = this.prepEndpoint("static/atten/attend");
    const data = [
      {
        stu_num: usernum,
        week: week,
      },
    ];
    return this.http.post(postAttendDataURL, data, httpOptions);
  }
  getAlluserData(): Observable<any> {
    const Url = this.prepEndpoint("static/admin/atten");
    return this.http.get(Url, httpOptions);
  }
  updateAdminAtten(json): Observable<any>{
    const url = this.prepEndpoint('static/admin/updateAtten');
    return this.http.post(url,json,httpOptions)
  }

  getAttenData(week): Observable<any> {
    const Url = this.prepEndpoint("static/admin/attenstatus");
    return this.http.post(Url, week, httpOptions);
  }


  prepEndpoint(ep) {
    return "http://localhost:9999/" + ep;
    //return ep;
  }
}
