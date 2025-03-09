import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InfoCompanyComponent } from './info-company.component';

describe('InfoCompanyComponent', () => {
  let component: InfoCompanyComponent;
  let fixture: ComponentFixture<InfoCompanyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InfoCompanyComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(InfoCompanyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
