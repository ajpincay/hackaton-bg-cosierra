import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InfoCertificationComponent } from './info-certification.component';

describe('InfoCertificationComponent', () => {
  let component: InfoCertificationComponent;
  let fixture: ComponentFixture<InfoCertificationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InfoCertificationComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(InfoCertificationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
