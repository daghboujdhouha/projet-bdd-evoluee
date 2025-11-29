import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { BookService, Book, BookFilters } from '../../services/book.service';

@Component({
  selector: 'app-books-page',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  template: `
    <div class="card">
      <h1>Liste des Livres</h1>
      
      <div style="margin-bottom: 20px; display: flex; gap: 10px; flex-wrap: wrap;">
        <input type="text" placeholder="Titre" [(ngModel)]="filters.title" (input)="search()" style="flex: 1; min-width: 200px;">
        <input type="text" placeholder="Auteur" [(ngModel)]="filters.author" (input)="search()" style="flex: 1; min-width: 200px;">
        <input type="text" placeholder="Genre" [(ngModel)]="filters.genre" (input)="search()" style="flex: 1; min-width: 200px;">
        <select [(ngModel)]="filters.status" (change)="search()" style="flex: 1; min-width: 150px;">
          <option value="">Tous les statuts</option>
          <option value="disponible">Disponible</option>
          <option value="réservé">Réservé</option>
          <option value="emprunté">Emprunté</option>
        </select>
        <button (click)="clearFilters()" class="btn btn-secondary">Réinitialiser</button>
      </div>

      <div *ngIf="loading" style="text-align: center; padding: 20px;">
        Chargement...
      </div>

      <div *ngIf="error" class="alert alert-error">
        {{ error }}
      </div>

      <div *ngIf="!loading && !error" class="books-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px;">
        <div *ngFor="let book of books" class="card" style="cursor: pointer;" (click)="viewBook(book.id)">
          <h3>{{ book.title }}</h3>
          <p><strong>Auteur:</strong> {{ book.author }}</p>
          <p><strong>Genre:</strong> {{ book.genre }}</p>
          <p><strong>Année:</strong> {{ book.year }}</p>
          <p><strong>Statut:</strong> 
            <span [style.color]="getStatusColor(book.status)">{{ book.status }}</span>
          </p>
        </div>
      </div>

      <div *ngIf="!loading && books.length === 0" class="alert alert-info">
        Aucun livre trouvé.
      </div>
    </div>
  `,
  styles: []
})
export class BooksPageComponent implements OnInit {
  books: Book[] = [];
  filters: BookFilters = {};
  loading = false;
  error = '';

  constructor(private bookService: BookService) {}

  ngOnInit(): void {
    this.loadBooks();
  }

  loadBooks(): void {
    this.loading = true;
    this.error = '';
    
    this.bookService.getBooks(this.filters).subscribe({
      next: (books) => {
        this.books = books;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Erreur lors du chargement des livres';
        this.loading = false;
      }
    });
  }

  search(): void {
    this.loadBooks();
  }

  clearFilters(): void {
    this.filters = {};
    this.loadBooks();
  }

  viewBook(id: string): void {
    window.location.href = `/books/${id}`;
  }

  getStatusColor(status: string): string {
    switch(status) {
      case 'disponible': return 'green';
      case 'réservé': return 'orange';
      case 'emprunté': return 'red';
      default: return 'black';
    }
  }
}

