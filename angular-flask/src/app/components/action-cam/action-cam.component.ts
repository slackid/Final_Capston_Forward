import {
  Component,
  ElementRef,
  OnInit,
  Renderer2,
  ViewChild,
} from "@angular/core";
import { AuthService } from "../../services/auth.service";

@Component({
  selector: "app-action-cam",
  templateUrl: "./action-cam.component.html",
  styleUrls: ["./action-cam.component.scss"],
})
export class ActionCamComponent implements OnInit {
  @ViewChild("video", { static: true }) videoElement: ElementRef;
  @ViewChild("canvas", { static: true }) canvas: ElementRef;

  constructor(private renderer: Renderer2, private authService: AuthService) {}
  constraints = {
    video: {
      facingMode: "environment",
      width: { ideal: 4096 },
      height: { ideal: 2160 },
    },
  };
  videoWidth = 0;
  videoHeight = 0;
  startcamera() {
    if (!!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)) {
      navigator.mediaDevices
        .getUserMedia(this.constraints)
        .then(this.attachVideo.bind(this))
        .catch(this.handleError);
    } else {
      alert("Sorry, camera not available.");
    }
  }

  handleError(error) {
    console.log("Error: ", error);
  }
  attachVideo(stream) {
    this.renderer.setProperty(
      this.videoElement.nativeElement,
      "srcObject",
      stream
    );
    this.renderer.listen(this.videoElement.nativeElement, "play", (event) => {
      this.videoHeight = this.videoElement.nativeElement.videoHeight;
      this.videoWidth = this.videoElement.nativeElement.videoWidth;
    });
  }
  capture() {
    this.renderer.setProperty(
      this.canvas.nativeElement,
      "width",
      this.videoWidth
    );
    this.renderer.setProperty(
      this.canvas.nativeElement,
      "height",
      this.videoHeight
    );
    this.canvas.nativeElement
      .getContext("2d")
      .drawImage(this.videoElement.nativeElement, 0, 0);
  }

  saveas() {
    var encdoeImage = this.canvas.nativeElement.toDataURL("image/png");

    const soulkey = JSON.stringify(encdoeImage);
    this.authService.sendImageDecode(soulkey).subscribe();
  }

  ngOnInit() {
    this.startcamera();
  }
}
