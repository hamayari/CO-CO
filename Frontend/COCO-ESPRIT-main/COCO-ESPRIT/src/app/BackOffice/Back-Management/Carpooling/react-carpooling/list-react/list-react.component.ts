import { AfterViewInit, Component, OnInit, ViewChild } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort, Sort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { ActivatedRoute, Router } from '@angular/router';
import { ReactCarpooling } from 'src/app/BackOffice/Back-Core/Models/Carpooling/react-carpooling';
import { ReactCarpoolingService } from 'src/app/BackOffice/Back-Core/Services/Carpooling/react-carpooling.service';

@Component({
  selector: 'app-list-react',
  templateUrl: './list-react.component.html',
  styleUrls: ['./list-react.component.css']
})
export class ListReactComponent implements AfterViewInit {
  displayedColumns: string[] = [
    'id',
    'user',
  ];
  compare(a: number | string, b: number | string, isAsc: boolean) {
    return (a < b ? -1 : 1) * (isAsc ? 1 : -1);
  }
  sortData($event: Sort) {
    if (!$event.active) {
      return;
    }
    this.data = this.data.sort((a, b) => {
      const isAsc = $event.direction === 'asc';
      if ($event.direction.length == 0) {
        return this.compare(
          a.idReactCarpooling,
          b.idReactCarpooling,
          !isAsc
        );
      }
      switch ($event.active) {
        case 'id':
          return this.compare(
            a.idReactCarpooling,
            b.idReactCarpooling,
            isAsc
          );
        case 'user':
          return this.compare(
            a.userReact.username,
            b.userReact.username,
            isAsc
          );


        default:
          return 0;
      }
    });

    this.dataSource.data = this.data;
  }
  OnViewProfile(arg0: any) {
    throw new Error('Method not implemented.');
  }
  data: ReactCarpooling[] = [];
  sortedData: ReactCarpooling[] = [];
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private formB: FormBuilder,
    private reactCarpoolingService: ReactCarpoolingService
  ) {
    /*this.reqCarpoolingService.listen().subscribe((m: any) => {
      this.loadData();
    });*/
  }

  ngOnInit() {
    this.loadData();
  }


  loadData() {
    this.reactCarpoolingService
      .getall()
      .subscribe((data: ReactCarpooling[]) => {
        this.reactCarpoolingService
          .getAllUsers()
          .subscribe(async (users: any[]) => {
            this.data = data.map((value, index, array) => {
              if (!value.userReact.id) {
                for (let index = 0; index < users.length; index++) {
                  const element = users[index];
                  if (
                    element.id.toString() == value.userReact.toString()
                  ) {
                    value.userReact = element;
                    break;
                  }
                }
              }
              return value;
            });
            this.totalReacts = data.length;
            this.dataSource = new MatTableDataSource(this.data);
            this.dataSource.sort = this.sort;
            this.dataSource.paginator = this.paginator;
          });
      }),
      (error: any) => {
        console.error('Error fetching user by ID:', error);
      };
  }

  totalReacts!: number;

  dataSource: MatTableDataSource<ReactCarpooling>;

  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  ngAfterViewInit() {}

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }
}
