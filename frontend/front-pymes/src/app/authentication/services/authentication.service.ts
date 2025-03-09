import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiResponseLoginUserI } from '../interfaces/authentication';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {
  //Variables
  urlApi: string = "https://s9c0tq03-8000.use2.devtunnels.ms";
  options = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json'
    })
  };

  //Constructor
  constructor(
    private http: HttpClient,
  ) { }

  //Método que consume el endpoint para iniciar sesión
  loginUser(body: any): Observable<ApiResponseLoginUserI> {
    return this.http.post<ApiResponseLoginUserI>(this.urlApi + "/auth/login", body);
  }
}
