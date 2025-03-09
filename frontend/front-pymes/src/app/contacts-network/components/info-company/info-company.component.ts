import { Component, Input } from '@angular/core';
import { companyRedI } from '../../interfaces/company-red';

@Component({
  selector: 'app-info-company',
  imports: [],
  templateUrl: './info-company.component.html',
  styleUrl: './info-company.component.css'
})
export class InfoCompanyComponent {
  @Input() arrayCompanies: companyRedI[] = [];
}
