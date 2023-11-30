<script>
document.addEventListener('DOMContentLoaded', function() {
  const body = document.body;
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

  if (prefersDark) {
    body.classList.remove('light-theme');
    body.classList.add('dark-theme');
    document.title = 'Тема сайту: Темна';
  } else {
    body.classList.remove('dark-theme');
    body.classList.add('light-theme');
    document.title = 'Тема сайту: Світла';
  }
});
</script>

<div align="center">
	<p>
		<a href="#"><img src="img/ist.png" width="600" alt="Information Security Technology" /></a>
	</p>
    <p>
        <a href="https://github.com/Yu-225/TZI/actions/workflows/release.yml"><img src="https://github.com/Yu-225/TZI/actions/workflows/release.yml/badge.svg" alt="Build and Release" /></a>
    </p>
	<p>
		<a href="https://github.com/Yu-225/TZI/actions/workflows/test.yml"><img src="https://github.com/Yu-225/TZI/actions/workflows/test.yml/badge.svg" alt="Test Lab 1" /></a>
    </p>
</div>




