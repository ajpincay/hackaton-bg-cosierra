import { Component } from '@angular/core';
import { SpinnerComponent } from '../../../shared-elements/components/spinner/spinner.component';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';

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

  //constrcutor
  constructor(

  ){}


  //Fomrulario de login
  loginForm = new FormGroup({
    email: new FormControl('', Validators.required),
    password: new FormControl('', Validators.required)
  })


  //Funcion para enviar el formulario
  loginUser() {
  }

}
