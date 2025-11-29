import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { AuthService } from './auth.service';

export interface Book {
  id: string;
  title: string;
  author: string;
  genre: string;
  year: number;
  description: string;
  isbn: string;
  status: string;
  created_at?: string;
  updated_at?: string;
}

export interface BookFilters {
  title?: string;
  author?: string;
  genre?: string;
  year?: number;
  isbn?: string;
  status?: string;
}

@Injectable({
  providedIn: 'root'
})
export class BookService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getBooks(filters?: BookFilters): Observable<Book[]> {
    let params = new HttpParams();
    
    if (filters) {
      if (filters.title) params = params.set('title', filters.title);
      if (filters.author) params = params.set('author', filters.author);
      if (filters.genre) params = params.set('genre', filters.genre);
      if (filters.year) params = params.set('year', filters.year.toString());
      if (filters.isbn) params = params.set('isbn', filters.isbn);
      if (filters.status) params = params.set('status', filters.status);
    }

    return this.http.get<Book[]>(`${this.apiUrl}/books`, { params });
  }

  getBook(id: string): Observable<Book> {
    return this.http.get<Book>(`${this.apiUrl}/books/${id}`);
  }

  createBook(book: Partial<Book>): Observable<Book> {
    return this.http.post<Book>(`${this.apiUrl}/books`, book);
  }

  updateBook(id: string, book: Partial<Book>): Observable<Book> {
    return this.http.put<Book>(`${this.apiUrl}/books/${id}`, book);
  }

  deleteBook(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/books/${id}`);
  }
}

