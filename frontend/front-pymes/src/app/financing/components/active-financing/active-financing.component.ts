import { Component, Input } from '@angular/core';
import { activeFinancingI } from '../../interfaces/active-financing';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-active-financing',
  imports: [
    CommonModule
  ],
  templateUrl: './active-financing.component.html',
  styleUrl: './active-financing.component.css'
})
export class ActiveFinancingComponent {
    //Variables
    @Input() arrayActivesFinancing: activeFinancingI[] = []
}
