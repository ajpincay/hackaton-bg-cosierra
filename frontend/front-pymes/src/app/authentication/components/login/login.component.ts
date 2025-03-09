import { Component } from '@angular/core';
import { SpinnerComponent } from '../../../shared-elements/components/spinner/spinner.component';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { ApiResponseLoginUserI } from '../../interfaces/authentication';
import { Router } from '@angular/router';
import { AuthenticationService } from '../../services/authentication.service';

@Component({
  selector: 'app-login',
  imports: [
    ReactiveFormsModule,
    FormsModule,
    SpinnerComponent,
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  //Variables
  spinnerStatus: boolean = false;

  //Constructor
  constructor(
    private router: Router,
    private authService: AuthenticationService,
  ) { }


  //Fomrulario de login
  loginForm = new FormGroup({
    ruc: new FormControl('', Validators.required),
    password: new FormControl('', Validators.required)
  })


  //Funcion para enviar el formulario
  loginUser() {
    this.spinnerStatus = true;
    if (this.loginForm.valid) {
      const body = {
        ruc: this.loginForm.value.ruc,
        password: this.loginForm.value.password
      };
      this.authService.loginUser(body)
        .subscribe({
          next: (res: ApiResponseLoginUserI) => {
            this.spinnerStatus = false;
            if (res) {
              this.router.navigateByUrl('/pyme/dashboard');
              console.log(res);
            }
            else{
              alert("Credenciales incorrectas");
            }
          }
        });
    } else {
      this.spinnerStatus = false;
      alert("Primero debe ingresar sus credenciales de acceso");
    }
  }

}
