import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { companyInfoI } from '../interfaces/company-red';

@Injectable({
  providedIn: 'root'
})
export class CompanyRedService {
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

  //Método que consume el endpoint para obtener la información de todas las PYMES disponibles para conectar
  getAllCompanies(ruc: string): Observable<companyInfoI[]> {
    return this.http.get<companyInfoI[]>(this.urlApi + `/network/${ruc}`, this.options);
  }
}
