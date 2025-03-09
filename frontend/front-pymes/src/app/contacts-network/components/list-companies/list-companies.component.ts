import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { MatTabsModule } from '@angular/material/tabs';

@Component({
  selector: 'app-list-companies',
  imports: [
    CommonModule,
    MatTabsModule
  ],
  templateUrl: './list-companies.component.html',
  styleUrl: './list-companies.component.css'
})
export class ListCompaniesComponent {
  //Variables
  activeTab: string = 'todas';

  changeTab(tab: string): void {
    this.activeTab = tab;
    console.log(this.activeTab);
  }
}
