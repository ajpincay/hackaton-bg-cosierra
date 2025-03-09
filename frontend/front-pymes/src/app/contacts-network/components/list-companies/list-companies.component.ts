import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { MatTabsModule } from '@angular/material/tabs';
import { companyRedI } from '../../interfaces/company-red';
import { InfoCompanyComponent } from "../info-company/info-company.component";

@Component({
  selector: 'app-list-companies',
  imports: [
    CommonModule,
    MatTabsModule,
    InfoCompanyComponent
],
  templateUrl: './list-companies.component.html',
  styleUrl: './list-companies.component.css'
})
export class ListCompaniesComponent {
  //Variables
  activeTab: string = 'todas';
  arrayAllCompanies: companyRedI[] = [
    {
      name: "Distribuidora Nacional S.A.",
      type: "Comercio",
      location: "Guayaquil, Guayas",
      rate: 85,
      conected: false,
      pending: false,
      details:{
          phone: "0999999999",
          email: "prueba@gmail.com",
          web: "www.prueba.com",
      }
    },
    {
      name: "Hamburguesas Al Carbón",
      type: "Restaurante",
      location: "Quevedo, Los Ríos",
      rate: 95,
      conected: false,
      pending: false,
      details:{
          phone: "0999999999",
          email: "prueba@gmail.com",
          web: "www.prueba.com",
      }
    },
    {
      name: "Taste Delicius",
      type: "Repostería",
      location: "Quevedo, Los Ríos",
      rate: 75,
      conected: false,
      pending: false,
      details:{
          phone: "0999999999",
          email: "prueba@gmail.com",
          web: "www.prueba.com",
      }
    },
    {
      name: "Rukito",
      type: "Restaurante",
      location: "Guayaquil, Guayas",
      rate: 100,
      conected: false,
      pending: false,
      details:{
          phone: "0999999999",
          email: "prueba@gmail.com",
          web: "www.prueba.com",
      }
    }
  ]

  arrayConectedCompanies: companyRedI[] = [
    {
      name: "Hamburguesas Al Carbón",
      type: "Restaurante",
      location: "Quevedo, Los Ríos",
      rate: 95,
      conected: true,
      pending: false,
      details:{
          phone: "0999999999",
          email: "prueba@gmail.com",
          web: "www.prueba.com",
      }
    },
    {
      name: "Rukito",
      type: "Restaurante",
      location: "Guayaquil, Guayas",
      rate: 100,
      conected: true,
      pending: false,
      details:{
          phone: "0999999999",
          email: "prueba@gmail.com",
          web: "www.prueba.com",
      }
    }
  ]

  arrayPendingCompanies: companyRedI[] = [
    {
      name: "Hamburguesas Al Carbón",
      type: "Restaurante",
      location: "Quevedo, Los Ríos",
      rate: 95,
      conected: false,
      pending: true,
      details:{
          phone: "0999999999",
          email: "prueba@gmail.com",
          web: "www.prueba.com",
      }
    },
    {
      name: "Rukito",
      type: "Restaurante",
      location: "Guayaquil, Guayas",
      rate: 100,
      conected: false,
      pending: true,
      details:{
          phone: "0999999999",
          email: "prueba@gmail.com",
          web: "www.prueba.com",
      }
    }
  ]
}
