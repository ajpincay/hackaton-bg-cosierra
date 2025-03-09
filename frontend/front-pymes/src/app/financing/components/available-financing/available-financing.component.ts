import { Component, Input } from '@angular/core';
import { availableFinancingI } from '../../interfaces/available-financing';


@Component({
  selector: 'app-available-financing',
  imports: [],
  templateUrl: './available-financing.component.html',
  styleUrl: './available-financing.component.css'
})
export class AvailableFinancingComponent {
  //Variables
  @Input() arrayAvailableFinancing: availableFinancingI[] = []
}
