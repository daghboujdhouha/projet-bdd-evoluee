import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface Borrow {
  id: string;
  user_id: string;
  book_id: string;
  borrow_date: string;
  return_date?: string;
  due_date: string;
  status: string;
  created_at?: string;
  updated_at?: string;
}

@Injectable({
  providedIn: 'root'
})
export class BorrowService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  createBorrow(bookId: string): Observable<Borrow> {
    return this.http.post<Borrow>(`${this.apiUrl}/borrows`, {
      book_id: bookId
    });
  }

  getBorrows(): Observable<Borrow[]> {
    return this.http.get<Borrow[]>(`${this.apiUrl}/borrows`);
  }

  getBorrow(id: string): Observable<Borrow> {
    return this.http.get<Borrow>(`${this.apiUrl}/borrows/${id}`);
  }

  returnBook(id: string): Observable<void> {
    return this.http.post<void>(`${this.apiUrl}/borrows/${id}/return`, {});
  }
}

