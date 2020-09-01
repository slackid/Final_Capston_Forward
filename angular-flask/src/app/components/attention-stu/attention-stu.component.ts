import { Component, OnInit } from "@angular/core";
import { Router } from "@angular/router";
import { FlashMessagesService } from "angular2-flash-messages";
import { AuthService } from "../../services/auth.service";
import { Attention } from "../../models/Attention";
@Component({
  selector: "app-attention-stu",
  templateUrl: "./attention-stu.component.html",
  styleUrls: ["./attention-stu.component.scss"],
})
export class AttentionStuComponent implements OnInit {
  constructor(
    private router: Router,
    private authService: AuthService,
    private flashMessage: FlashMessagesService
  ) {}
  fullImagePath: string;
  converted_image: string;
  Attentionlist = [
    new Attention(1, "2020.8.30", "On"),
    new Attention(2, "2020.11.11", "ON"),
    new Attention(3, "2020.11.14", "OFF"),
    new Attention(4, "2020.11.15", "ON"),
    new Attention(5, "2020.11.16", "ON"),
    new Attention(6, "2020.11.17", "ON"),
    new Attention(7, "2020.11.18", "ON"),
    new Attention(8, "2020.11.9", "ON"),
    new Attention(9, "2020.11.20", "ON"),
    new Attention(10, "2020.11.21", "ON"),
    new Attention(11, "2020.11.22", "ON"),
    new Attention(12, "2020.11.23", "ON"),
  ];

  //출결 , 날짜, 주차 , 이미지 (GET , POST )
  ngOnInit(): void {}
  clicked(number) {
    var asd;
    var dsd;
    var usernum;
    var username;
    dsd = localStorage.getItem("user");
    asd = this.Attentionlist[number - 1].date;
    console.log(this.Attentionlist[number - 1].date);
    usernum = JSON.parse(dsd).stu_num;
    username = JSON.parse(dsd).name;
    var cdcd;
    this.authService
      .getImageEncdoe(usernum, username, asd)
      .subscribe((data) => {
        cdcd = data["msg"];
        this.converted_image = "data:image/jpeg;base64," + cdcd;
      });
  }

  checkLoggedIn() {
    return this.authService.loggedIn();
  }
}
