import { Component } from '@angular/core';
import { DashboardService } from '../../services/dashboard.service';
import { ApiResponseDashboardI } from '../../interfaces/dashboard';
import { SpinnerComponent } from '../spinner/spinner.component';

@Component({
  selector: 'app-sumary-options',
  imports: [
    SpinnerComponent
  ],
  templateUrl: './sumary-options.component.html',
  styleUrl: './sumary-options.component.css'
})
export class SumaryOptionsComponent {
  //Variables
  spinnerStatus: boolean = false;
  infoDashboard: ApiResponseDashboardI = {} as ApiResponseDashboardI;

  constructor(
    private dashboardService: DashboardService
  ){}

  //ngOnInit
  ngOnInit(){
    this.spinnerStatus = true;
    this.dashboardService.getInfoDashboard(sessionStorage.getItem('ruc'))
    .subscribe((data) => {
      this.infoDashboard = data;
      this.spinnerStatus = false
    });
  }
}
