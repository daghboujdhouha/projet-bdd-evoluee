import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { AuthService, User } from '../../services/auth.service';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <nav style="background-color: #007bff; color: white; padding: 1rem;">
      <div class="container" style="display: flex; justify-content: space-between; align-items: center;">
        <div>
          <a routerLink="/books" style="color: white; text-decoration: none; font-size: 1.5rem; font-weight: bold;">
            📚 Bibliothèque Numérique
          </a>
        </div>
        <div style="display: flex; gap: 1rem; align-items: center;">
          <ng-container *ngIf="currentUser; else notLoggedIn">
            <span>Bonjour, {{ currentUser.username }} ({{ currentUser.role }})</span>
            <a routerLink="/books" style="color: white; text-decoration: none;">Livres</a>
            <a routerLink="/reservations" style="color: white; text-decoration: none;">Mes Réservations</a>
            <a routerLink="/borrows" style="color: white; text-decoration: none;">Mes Emprunts</a>
            <a *ngIf="currentUser.role === 'admin'" routerLink="/admin" style="color: white; text-decoration: none;">Admin</a>
            <button (click)="logout()" class="btn" style="background-color: #dc3545; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">
              Déconnexion
            </button>
          </ng-container>
          <ng-template #notLoggedIn>
            <a routerLink="/login" style="color: white; text-decoration: none;">Connexion</a>
            <a routerLink="/register" style="color: white; text-decoration: none;">Inscription</a>
          </ng-template>
        </div>
      </div>
    </nav>
  `,
  styles: []
})
export class NavbarComponent implements OnInit {
  currentUser: User | null = null;

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.authService.currentUser$.subscribe(user => {
      this.currentUser = user;
    });
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}

