import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ReservationService, Reservation } from '../../services/reservation.service';
import { BookService, Book } from '../../services/book.service';

@Component({
  selector: 'app-reservations-page',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="card">
      <h1>Mes Réservations</h1>

      <div *ngIf="loading" style="text-align: center; padding: 20px;">
        Chargement...
      </div>

      <div *ngIf="error" class="alert alert-error">
        {{ error }}
      </div>

      <div *ngIf="message" class="alert" [ngClass]="messageType === 'success' ? 'alert-success' : 'alert-error'">
        {{ message }}
      </div>

      <table *ngIf="!loading && reservations.length > 0" class="table">
        <thead>
          <tr>
            <th>Livre</th>
            <th>Date de réservation</th>
            <th>Date d'expiration</th>
            <th>Statut</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr *ngFor="let reservation of reservations">
            <td>{{ getBookTitle(reservation.book_id) }}</td>
            <td>{{ formatDate(reservation.reservation_date) }}</td>
            <td>{{ formatDate(reservation.expiry_date) }}</td>
            <td>{{ reservation.status }}</td>
            <td>
              <button 
                *ngIf="reservation.status === 'active'"
                (click)="cancelReservation(reservation.id)" 
                class="btn btn-danger"
                [disabled]="actionLoading">
                Annuler
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div *ngIf="!loading && reservations.length === 0" class="alert alert-info">
        Vous n'avez aucune réservation.
      </div>
    </div>
  `,
  styles: []
})
export class ReservationsPageComponent implements OnInit {
  reservations: Reservation[] = [];
  books: Map<string, Book> = new Map();
  loading = false;
  error = '';
  message = '';
  messageType: 'success' | 'error' = 'success';
  actionLoading = false;

  constructor(
    private reservationService: ReservationService,
    private bookService: BookService
  ) {}

  ngOnInit(): void {
    this.loadReservations();
  }

  loadReservations(): void {
    this.loading = true;
    this.error = '';
    
    this.reservationService.getReservations().subscribe({
      next: (reservations) => {
        this.reservations = reservations;
        this.loadBookTitles();
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Erreur lors du chargement des réservations';
        this.loading = false;
      }
    });
  }

  loadBookTitles(): void {
    const bookIds = [...new Set(this.reservations.map(r => r.book_id))];
    bookIds.forEach(id => {
      this.bookService.getBook(id).subscribe({
        next: (book) => {
          this.books.set(id, book);
        }
      });
    });
  }

  cancelReservation(id: string): void {
    this.actionLoading = true;
    this.message = '';
    
    this.reservationService.cancelReservation(id).subscribe({
      next: () => {
        this.message = 'Réservation annulée avec succès';
        this.messageType = 'success';
        this.actionLoading = false;
        this.loadReservations();
      },
      error: (err) => {
        this.message = err.error?.error || 'Erreur lors de l\'annulation';
        this.messageType = 'error';
        this.actionLoading = false;
      }
    });
  }

  getBookTitle(bookId: string): string {
    return this.books.get(bookId)?.title || 'Chargement...';
  }

  formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString('fr-FR');
  }
}

