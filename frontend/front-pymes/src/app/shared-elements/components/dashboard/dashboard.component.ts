import { Component, ElementRef } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { SpinnerComponent } from '../spinner/spinner.component';

@Component({
  selector: 'app-dashboard',
  imports: [
    RouterModule,
    SpinnerComponent
  ],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent {
  //Variables
  spinnerStatus: boolean = false;

  constructor(
    private router: Router,
    private elementRef: ElementRef
  ) { }


  //Método que redirige al usuario al inicio según el perfil
  goToHome() {
    this.router.navigateByUrl('pyme/dashboard');
  }

  //Método que cierra la sesión del usuario
  signOut() {
    this.spinnerStatus = true;
    setTimeout(() => {
      this.spinnerStatus = false;
      this.router.navigateByUrl('authentication/login');
    }, 1500);
  }

  // Método que muestra y oculta el manú lateral del dashboard
  showHideSidebar() {
    const sidebar = this.elementRef.nativeElement.querySelector('#sidebar');
    if (sidebar) { // Verificamos si sidebar existe
      sidebar.classList.toggle('hide');
    }
  }
}
