import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import { Observable } from 'rxjs';
import { ApiResponseDashboardI } from '../interfaces/dashboard';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {
    //Variables
    urlApi: string = environment.URL_API;
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
    getInfoDashboard(ruc: any): Observable<ApiResponseDashboardI> {
      return this.http.get<ApiResponseDashboardI>(this.urlApi + `/dashboard/${ruc}`, this.options);
    }
}
