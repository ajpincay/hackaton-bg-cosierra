import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HistoryFinancingComponent } from './history-financing.component';

describe('HistoryFinancingComponent', () => {
  let component: HistoryFinancingComponent;
  let fixture: ComponentFixture<HistoryFinancingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HistoryFinancingComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(HistoryFinancingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
