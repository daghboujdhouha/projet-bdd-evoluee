import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { BookService, Book } from '../../services/book.service';
import { ReservationService } from '../../services/reservation.service';
import { BorrowService } from '../../services/borrow.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-book-detail-page',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div *ngIf="loading" style="text-align: center; padding: 20px;">
      Chargement...
    </div>

    <div *ngIf="error" class="alert alert-error">
      {{ error }}
    </div>

    <div *ngIf="book && !loading" class="card">
      <button (click)="goBack()" class="btn btn-secondary" style="margin-bottom: 20px;">
        ← Retour
      </button>
      
      <h1>{{ book.title }}</h1>
      <p><strong>Auteur:</strong> {{ book.author }}</p>
      <p><strong>Genre:</strong> {{ book.genre }}</p>
      <p><strong>Année:</strong> {{ book.year }}</p>
      <p><strong>ISBN:</strong> {{ book.isbn }}</p>
      <p><strong>Statut:</strong> 
        <span [style.color]="getStatusColor(book.status)">{{ book.status }}</span>
      </p>
      <p><strong>Description:</strong></p>
      <p>{{ book.description }}</p>

      <div *ngIf="message" class="alert" [ngClass]="messageType === 'success' ? 'alert-success' : 'alert-error'">
        {{ message }}
      </div>

      <div style="margin-top: 20px; display: flex; gap: 10px;">
        <button 
          *ngIf="book.status === 'disponible' && !isAdmin()" 
          (click)="reserveBook()" 
          class="btn btn-primary"
          [disabled]="actionLoading">
          Réserver
        </button>
        <button 
          *ngIf="(book.status === 'disponible' || book.status === 'réservé') && !isAdmin()" 
          (click)="borrowBook()" 
          class="btn btn-primary"
          [disabled]="actionLoading">
          Emprunter
        </button>
      </div>
    </div>
  `,
  styles: []
})
export class BookDetailPageComponent implements OnInit {
  book: Book | null = null;
  loading = false;
  error = '';
  message = '';
  messageType: 'success' | 'error' = 'success';
  actionLoading = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private bookService: BookService,
    private reservationService: ReservationService,
    private borrowService: BorrowService,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.loadBook(id);
    }
  }

  loadBook(id: string): void {
    this.loading = true;
    this.error = '';
    
    this.bookService.getBook(id).subscribe({
      next: (book) => {
        this.book = book;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Livre non trouvé';
        this.loading = false;
      }
    });
  }

  reserveBook(): void {
    if (!this.book) return;
    
    this.actionLoading = true;
    this.message = '';
    
    this.reservationService.createReservation(this.book.id).subscribe({
      next: () => {
        this.message = 'Livre réservé avec succès';
        this.messageType = 'success';
        this.actionLoading = false;
        this.loadBook(this.book!.id);
      },
      error: (err) => {
        this.message = err.error?.error || 'Erreur lors de la réservation';
        this.messageType = 'error';
        this.actionLoading = false;
      }
    });
  }

  borrowBook(): void {
    if (!this.book) return;
    
    this.actionLoading = true;
    this.message = '';
    
    this.borrowService.createBorrow(this.book.id).subscribe({
      next: () => {
        this.message = 'Livre emprunté avec succès';
        this.messageType = 'success';
        this.actionLoading = false;
        this.loadBook(this.book!.id);
      },
      error: (err) => {
        this.message = err.error?.error || 'Erreur lors de l\'emprunt';
        this.messageType = 'error';
        this.actionLoading = false;
      }
    });
  }

  goBack(): void {
    this.router.navigate(['/books']);
  }

  getStatusColor(status: string): string {
    switch(status) {
      case 'disponible': return 'green';
      case 'réservé': return 'orange';
      case 'emprunté': return 'red';
      default: return 'black';
    }
  }

  isAdmin(): boolean {
    return this.authService.isAdmin();
  }
}

