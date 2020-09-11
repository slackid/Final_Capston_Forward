import { Injectable } from "@angular/core";

@Injectable()
export class ValidateService {
  constructor() {}

  validateRegister(user) {
    if (
      user.name == undefined ||
      user.email == undefined ||
      user.stu_num == undefined ||
      user.password == undefined
    ) {
      return false;
    } else {
      return true;
    }
  }

  validateAdminRegister(admin) {
    if (
      admin.admin_num == undefined ||
      admin.password == undefined
    ) {
      return false;
    } else {
      return true;
    }
  }

  validateEmail(email) {
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
  }
}
