import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { MatTabsModule } from '@angular/material/tabs';
import { companyInfoI, companyRedI } from '../../interfaces/company-red';
import { InfoCompanyComponent } from "../info-company/info-company.component";
import { CompanyRedService } from '../../services/company-red.service';
import { SpinnerComponent } from '../../../shared-elements/components/spinner/spinner.component';

@Component({
  selector: 'app-list-companies',
  imports: [
    CommonModule,
    MatTabsModule,
    InfoCompanyComponent,
    SpinnerComponent
],
  templateUrl: './list-companies.component.html',
  styleUrl: './list-companies.component.css'
})
export class ListCompaniesComponent {
  //Variables
  spinnerStatus: boolean = false;
  activeTab: string = 'todas';
  /* arrayAllCompanies: companyRedI[] = [
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
  ] */

  arrayAllCompanies: companyInfoI[] = [];

  arrayConectedCompanies: companyInfoI[] = [
    {
      ruc: "1045568214",
      pyme_name: "Georgina_Georgina S.A.",
      sector: "PRIVADO",
      location: "ESMERALDAS",
      peer_review: 0,
      connected: false,
      pending: false
    },
    {
      ruc: "1045568214",
      pyme_name: "Georgina_Georgina S.A.",
      sector: "PRIVADO",
      location: "ESMERALDAS",
      peer_review: 0,
      connected: false,
      pending: false
    },
  ]

  arrayPendingCompanies: companyInfoI[] = [
    {
      ruc: "1045568214",
      pyme_name: "Georgina_Georgina S.A.",
      sector: "PRIVADO",
      location: "ESMERALDAS",
      peer_review: 0,
      connected: false,
      pending: true
    },
    {
      ruc: "1045568214",
      pyme_name: "Pronaca S.A.",
      sector: "PRIVADO",
      location: "ESMERALDAS",
      peer_review: 0,
      connected: false,
      pending: true
    },
    {
      ruc: "1045568214",
      pyme_name: "Burritos S.A.",
      sector: "PRIVADO",
      location: "ESMERALDAS",
      peer_review: 0,
      connected: false,
      pending: true
    },
  ]

  //constructor
  constructor(
    private companyRedService: CompanyRedService
  ){}

  //ngOnInit
  ngOnInit(): void {
    this.spinnerStatus = true;
    const ruc = sessionStorage.getItem('ruc') || "1019283518";

    this.companyRedService.getAllCompanies(ruc).subscribe({
        next: (res: companyInfoI[]) => {
            this.spinnerStatus = false;
            if (res && res.length > 0) {
                this.arrayAllCompanies = res;
                console.log(this.arrayAllCompanies);
            } else {
                alert("No se encontraron empresas registradas con este RUC.");
            }
        },
        error: (err) => {
            this.spinnerStatus = false;
            console.error("Error al obtener las empresas:", err);
            alert("Ocurrió un error al obtener los datos. Intente nuevamente.");
        }
    });
}

}
