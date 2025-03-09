import { Component, Input } from '@angular/core';
import { certificationsI } from '../../interfaces/certifications';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-info-certification',
  imports: [
    CommonModule
  ],
  templateUrl: './info-certification.component.html',
  styleUrl: './info-certification.component.css'
})
export class InfoCertificationComponent {
   //Variables
      @Input() arrayCertifications: certificationsI[] = []
}
