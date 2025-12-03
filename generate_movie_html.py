import csv
import os

def generate_html():
    movies = []
    csv_file = 'movie.csv'
    
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found.")
        return

    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies.append(row)

    html_content = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>精選電影清單</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #141414;
            color: #ffffff;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }
        .navbar {
            background-color: #000000;
            padding: 20px;
        }
        .navbar-brand {
            color: #e50914 !important;
            font-size: 24px;
            font-weight: bold;
        }
        .movie-card {
            background-color: #2f2f2f;
            border: none;
            transition: transform 0.3s;
            height: 100%;
            cursor: pointer;
            border-radius: 8px;
            overflow: hidden;
        }
        .movie-card:hover {
            transform: scale(1.05);
            z-index: 10;
            box-shadow: 0 10px 20px rgba(0,0,0,0.5);
        }
        .card-img-top {
            height: 400px;
            object-fit: cover;
        }
        .card-body {
            padding: 15px;
        }
        .card-title {
            font-size: 1.1rem;
            font-weight: bold;
            margin-bottom: 10px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .card-text {
            font-size: 0.9rem;
            color: #b3b3b3;
        }
        .rating-badge {
            position: absolute;
            top: 10px;
            right: 10px;
            background-color: rgba(0, 0, 0, 0.7);
            color: #ffc107;
            padding: 5px 10px;
            border-radius: 4px;
            font-weight: bold;
        }
        .modal-content {
            background-color: #181818;
            color: white;
        }
        .modal-header {
            border-bottom: 1px solid #333;
        }
        .modal-footer {
            border-top: 1px solid #333;
        }
        .btn-close {
            filter: invert(1) grayscale(100%) brightness(200%);
        }
        .movie-detail-img {
            width: 100%;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        }
        .detail-label {
            color: #777;
            font-weight: bold;
            margin-right: 10px;
        }
    </style>
</head>
<body>

    <nav class="navbar navbar-dark">
        <div class="container">
            <a class="navbar-brand" href="#">🎬 MovieCollection</a>
        </div>
    </nav>

    <div class="container py-5">
        <h2 class="mb-4 border-start border-4 border-danger ps-3">熱門電影</h2>
        <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4">
    """

    for i, movie in enumerate(movies):
        # Handle potential missing keys gracefully
        name = movie.get('name', 'Unknown')
        image_url = movie.get('image_url', '')
        rating = movie.get('rating', 'N/A')
        categories = movie.get('categories', '')
        region = movie.get('region', '')
        duration = movie.get('release_date', '') # Based on CSV inspection, this column holds duration
        
        # Create a unique ID for the modal
        modal_id = f"movieModal{i}"
        
        html_content += f"""
            <div class="col">
                <div class="card movie-card" data-bs-toggle="modal" data-bs-target="#{modal_id}">
                    <span class="rating-badge">★ {rating}</span>
                    <img src="{image_url}" class="card-img-top" alt="{name}" onerror="this.src='https://via.placeholder.com/300x450?text=No+Image'">
                    <div class="card-body">
                        <h5 class="card-title" title="{name}">{name}</h5>
                        <p class="card-text">{categories}</p>
                    </div>
                </div>
            </div>

            <!-- Modal -->
            <div class="modal fade" id="{modal_id}" tabindex="-1" aria-hidden="true">
                <div class="modal-dialog modal-lg modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">{name}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row">
                                <div class="col-md-5">
                                    <img src="{image_url}" class="movie-detail-img mb-3 mb-md-0" alt="{name}">
                                </div>
                                <div class="col-md-7">
                                    <h3 class="mb-3">{name}</h3>
                                    <p><span class="detail-label">評分:</span> <span class="text-warning">★ {rating}</span></p>
                                    <p><span class="detail-label">類型:</span> {categories}</p>
                                    <p><span class="detail-label">地區:</span> {region}</p>
                                    <p><span class="detail-label">片長/上映:</span> {duration}</p>
                                    <hr>
                                    <p class="text-muted">
                                        這是一部來自 {region} 的精彩電影，獲得了 {rating} 的高分評價。
                                        屬於 {categories} 類型。
                                    </p>
                                    <a href="{movie.get('url', '#')}" target="_blank" class="btn btn-danger mt-3">查看更多詳情</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        """

    html_content += """
        </div>
    </div>

    <footer class="text-center py-4 text-muted">
        <p>&copy; 2025 MovieCollection. All rights reserved.</p>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
    """

    with open('movie.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Successfully generated movie.html")

if __name__ == "__main__":
    generate_html()
