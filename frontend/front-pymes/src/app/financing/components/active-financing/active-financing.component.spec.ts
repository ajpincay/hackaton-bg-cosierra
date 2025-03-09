import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ActiveFinancingComponent } from './active-financing.component';

describe('ActiveFinancingComponent', () => {
  let component: ActiveFinancingComponent;
  let fixture: ComponentFixture<ActiveFinancingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ActiveFinancingComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ActiveFinancingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
