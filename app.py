import streamlit as st
import streamlit.components.v1 as components
import base64

# 1. 페이지 설정
st.set_page_config(page_title="3D 도형 변신 앱", layout="wide")

# 2. 사이드바 UI 구성
st.sidebar.title("🛠️ 설정")

# 도형 선택 버튼 (라디오 버튼 사용)
selected_shape = st.sidebar.radio(
    "도형 모양을 선택하세요:",
    ("정육면체 (Cube)", "구 (Sphere)", "사각기둥 (Box)", "원기둥 (Cylinder)", "각뿔 (Pyramid)")
)

# 이미지 업로드 버튼
uploaded_file = st.sidebar.file_uploader("텍스처 이미지 업로드", type=['png', 'jpg', 'jpeg'])

st.title(f"🧊 {selected_shape} 뷰어")
st.write("왼쪽 사이드바에서 도형을 바꾸거나 사진을 입혀보세요!")

# 3. 이미지 데이터 처리 (Base64 변환)
texture_data = "null" # 기본값 (이미지 없음)

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    base64_str = base64.b64encode(bytes_data).decode()
    mime_type = uploaded_file.type
    texture_data = f"'data:{mime_type};base64,{base64_str}'"

# 4. 도형 종류를 JS로 넘기기 위한 문자열 매핑
# 파이썬의 선택값을 자바스크립트가 알아들을 수 있는 영문 키워드로 변환
shape_map = {
    "정육면체 (Cube)": "cube",
    "구 (Sphere)": "sphere",
    "사각기둥 (Box)": "rect",
    "원기둥 (Cylinder)": "cylinder",
    "각뿔 (Pyramid)": "pyramid"
}
current_shape = shape_map[selected_shape]

# 5. HTML/JS 코드 (Three.js)
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

        // --- 파이썬에서 받은 변수들 ---
        const shapeType = '{current_shape}';  // 도형 종류
        const textureUrl = {texture_data};    // 이미지 데이터

        // --- 씬 설정 ---
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0E1117);

        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.z = 4.5;

        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // --- 조명 추가 (이미지가 더 잘 보이게) ---
        const ambientLight = new THREE.AmbientLight(0xffffff, 1); // 전체 조명
        scene.add(ambientLight);

        // --- 도형 생성 로직 (Switch 문) ---
        let geometry;

        switch (shapeType) {{
            case 'cube':
                geometry = new THREE.BoxGeometry(2, 2, 2); // 정육면체
                break;
            case 'sphere':
                geometry = new THREE.SphereGeometry(1.5, 32, 32); // 구 (매끈하게)
                break;
            case 'rect':
                geometry = new THREE.BoxGeometry(1.5, 3, 1.5); // 사각기둥 (길쭉하게)
                break;
            case 'cylinder':
                geometry = new THREE.CylinderGeometry(1, 1, 3, 32); // 원기둥
                break;
            case 'pyramid':
                // ConeGeometry에서 면(radialSegments)을 4로 하면 피라미드가 됨
                geometry = new THREE.ConeGeometry(1.8, 2.5, 4); 
                break;
            default:
                geometry = new THREE.BoxGeometry(2, 2, 2);
        }}

        // --- 재질(텍스처) 설정 로직 ---
        let material;
        if (textureUrl) {{
            // 이미지가 있을 때
            const loader = new THREE.TextureLoader();
            const texture = loader.load(textureUrl);
            texture.colorSpace = THREE.SRGBColorSpace;
            material = new THREE.MeshBasicMaterial({{ map: texture }});
        }} else {{
            // 이미지가 없을 때 (기본 무지개색)
            material = new THREE.MeshNormalMaterial(); 
        }}

        // --- 메쉬 생성 및 추가 ---
        const mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);

        // --- 컨트롤 설정 ---
        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;

        // --- 애니메이션 ---
        function animate() {{
            requestAnimationFrame(animate);
            
            // 살짝 회전
            mesh.rotation.x += 0.005;
            mesh.rotation.y += 0.005;

            controls.update();
            renderer.render(scene, camera);
        }}

        // --- 반응형 창 크기 ---
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

# 6. 화면 출력
components.html(html_code, height=700)
