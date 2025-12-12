import streamlit as st
import streamlit.components.v1 as components
import base64

# 1. 페이지 설정
st.set_page_config(page_title="3D 도형 마스터", layout="wide")

# 2. 사이드바 설정
st.sidebar.title("🛠️ 도형 공방")

# 도형 선택 버튼 (정다면체 5개 + 기타 도형)
selected_shape = st.sidebar.radio(
    "도형을 선택하세요:",
    (
        "정사면체 (Tetrahedron)", 
        "정육면체 (Cube)", 
        "정팔면체 (Octahedron)", 
        "정십이면체 (Dodecahedron)", 
        "정이십면체 (Icosahedron)", 
        "구 (Sphere)", 
        "원기둥 (Cylinder)", 
        "사각기둥 (Box)", 
        "각뿔 (Pyramid)"
    )
)

# 이미지 업로더
uploaded_file = st.sidebar.file_uploader("텍스처(스킨) 입히기", type=['png', 'jpg', 'jpeg'])

st.title(f"🧊 {selected_shape} 뷰어")
st.write("모든 정다면체와 기본 도형을 3D로 돌려보세요.")

# 3. 이미지 데이터 처리
texture_data = "null"

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    base64_str = base64.b64encode(bytes_data).decode()
    mime_type = uploaded_file.type
    texture_data = f"'data:{mime_type};base64,{base64_str}'"

# 4. 파이썬 선택값 -> 자바스크립트 키워드 매핑
shape_map = {
    "정사면체 (Tetrahedron)": "tetrahedron",
    "정육면체 (Cube)": "cube",
    "정팔면체 (Octahedron)": "octahedron",
    "정십이면체 (Dodecahedron)": "dodecahedron",
    "정이십면체 (Icosahedron)": "icosahedron",
    "구 (Sphere)": "sphere",
    "원기둥 (Cylinder)": "cylinder",
    "사각기둥 (Box)": "rect",
    "각뿔 (Pyramid)": "pyramid"
}
current_shape = shape_map[selected_shape]

# 5. HTML/JS 코드 작성
html_code = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <style>
        body {{ margin: 0; overflow: hidden; background-color: #0E1117; }}
        canvas {{ width: 100%; height: 100%; }}
    </style>
</head>
<body>
    <script type="importmap">
        {{
            "imports": {{
                "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
                "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
            }}
        }}
    </script>
    <script type="module">
        import * as THREE from 'three';
        import {{ OrbitControls }} from 'three/addons/controls/OrbitControls.js';

        // 파이썬 변수 주입
        const shapeType = '{current_shape}';
        const textureUrl = {texture_data};

        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0E1117);

        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.z = 4.5;

        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        const ambientLight = new THREE.AmbientLight(0xffffff, 1);
        scene.add(ambientLight);
        
        // 입체감을 더 살리기 위한 방향성 조명 추가
        const dirLight = new THREE.DirectionalLight(0xffffff, 0.5);
        dirLight.position.set(5, 5, 5);
        scene.add(dirLight);

        // --- 도형 생성 로직 ---
        let geometry;
        const radius = 1.8; // 기본 크기

        switch (shapeType) {{
            // [정다면체 5형제]
            case 'tetrahedron': // 정사면체
                geometry = new THREE.TetrahedronGeometry(radius);
                break;
            case 'cube':        // 정육면체
                geometry = new THREE.BoxGeometry(2.5, 2.5, 2.5);
                break;
            case 'octahedron':  // 정팔면체
                geometry = new THREE.OctahedronGeometry(radius);
                break;
            case 'dodecahedron':// 정십이면체
                geometry = new THREE.DodecahedronGeometry(radius);
                break;
            case 'icosahedron': // 정이십면체
                geometry = new THREE.IcosahedronGeometry(radius);
                break;
            
            // [기타 도형]
            case 'sphere':
                geometry = new THREE.SphereGeometry(radius, 32, 32);
                break;
            case 'cylinder':
                geometry = new THREE.CylinderGeometry(1, 1, 3, 32);
                break;
            case 'rect':
                geometry = new THREE.BoxGeometry(1.5, 3, 1.5);
                break;
            case 'pyramid':
                geometry = new THREE.ConeGeometry(1.8, 2.5, 4); // 밑면이 사각형인 각뿔
                break;
            default:
                geometry = new THREE.BoxGeometry(2, 2, 2);
        }}

        // --- 재질 설정 ---
        let material;
        if (textureUrl) {{
            const loader = new THREE.TextureLoader();
            const texture = loader.load(textureUrl);
            texture.colorSpace = THREE.SRGBColorSpace;
            material = new THREE.MeshStandardMaterial({{ map: texture, roughness: 0.3 }});
        }} else {{
            // 이미지가 없으면 빛 반사가 예쁜 재질로 변경
            material = new THREE.MeshNormalMaterial();
        }}

        const mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);

        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;

        function animate() {{
            requestAnimationFrame(animate);
            mesh.rotation.x += 0.005;
            mesh.rotation.y += 0.005;
            controls.update();
            renderer.render(scene, camera);
        }}

        window.addEventListener('resize', function() {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});

        animate();
    </script>
</body>
</html>
"""

components.html(html_code, height=700)
