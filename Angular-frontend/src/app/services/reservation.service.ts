import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface Reservation {
  id: string;
  user_id: string;
  book_id: string;
  reservation_date: string;
  expiry_date: string;
  status: string;
  created_at?: string;
  updated_at?: string;
}

@Injectable({
  providedIn: 'root'
})
export class ReservationService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  createReservation(bookId: string): Observable<Reservation> {
    return this.http.post<Reservation>(`${this.apiUrl}/reservations`, {
      book_id: bookId
    });
  }

  getReservations(): Observable<Reservation[]> {
    return this.http.get<Reservation[]>(`${this.apiUrl}/reservations`);
  }

  getReservation(id: string): Observable<Reservation> {
    return this.http.get<Reservation>(`${this.apiUrl}/reservations/${id}`);
  }

  cancelReservation(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/reservations/${id}`);
  }
}

